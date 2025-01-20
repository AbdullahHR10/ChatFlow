from website import socketio
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from website.models.user import User
from website.models.message import Message
from website.models.conversation import Conversation
from website.models.group import Group, GroupMembership
from website.models.notification import Notification
from website import db
from datetime import datetime

import pytz


@socketio.on('connect')
def user_connected():
    """
    Handles a new socket connection when a user connects to the server.

    - Checks if the user is authenticated.
    - Updates the user's status to 'online'
        and updates the last seen timestamp.
    - Retrieves all conversations that the user is a part of
        (either as user1 or user2).
    - Retrieves all groups the user is a member of.
    - Joins the corresponding rooms for each conversation and group
        to receive real-time updates.
    - Emits the chat history for each conversation and group.
    """
    if current_user.is_authenticated:
        # Update user's status to 'online' and set the 'last_seen' timestamp
        current_user.status = 'online'
        current_user.last_seen = datetime.now(pytz.utc)
        db.session.commit()

        # Retrieve all conversations the user is part of
        conversations = Conversation.query.filter(
            (Conversation.user1_id == current_user.id) |
            (Conversation.user2_id == current_user.id)
        ).all()

        # Retrieve all groups the user is a member of
        groups = Group.query.join(Group.group_members).filter(
            GroupMembership.user_id == current_user.id
        ).all()

        # Iterate through each conversation the user is part of
        for conversation in conversations:
            # Join the conversation room using the conversation ID
            join_room(f'conversation_{conversation.id}')

            # Fetch all messages for the current conversation
            messages = Message.query.filter_by(
                conversation_id=conversation.id
            ).order_by(Message.timestamp).all()

            # Prepare the message data to be sent as a list of dictionaries
            messages_data = [{'message': msg.content,
                              'sender_id': msg.sender_id,
                              'timestamp': msg.timestamp.isoformat()}
                             for msg in messages]

            # Emit the chat history to the client for the specific conversation
            emit('chat_history',
                 {'conversation_id': conversation.id,
                  'messages': messages_data},
                 room=f'conversation_{conversation.id}')

        # Iterate through each group the user is a member of
        for group in groups:
            # Join the group room using the group ID
            join_room(f'group_{group.id}')

            # Fetch all messages for the current group
            group_messages = Message.query.filter_by(
                conversation_id=group.id
            ).order_by(Message.timestamp).all()

            # Prepare the message data for groups to be sent
            group_messages_data = [{'message': msg.content,
                                    'sender_id': msg.sender_id,
                                    'timestamp': msg.timestamp.isoformat()}
                                   for msg in group_messages]

            # Emit the chat history to the client for the specific group
            emit('group_chat_history',
                 {'group_id': group.id,
                  'messages': group_messages_data},
                 room=f'group_{group.id}')

        # Emit the user's online status to all connected clients,
        # broadcasting the status update
        emit('status_update',
             {'user_id': current_user.id, 'status': 'online'}, broadcast=True)


@socketio.on('disconnect')
def user_disconnected():
    """
    Handles socket disconnection when a user disconnects from the server.

    - Checks if the user is authenticated.
    - Updates the user's status to 'offline' and sets the last seen timestamp.
    - Commits the changes to the database.
    - Retrieves all conversations the user is part of
        (either as user1 or user2).
    - Removes the user from the corresponding rooms for each conversation.
    - Emits the user's updated status ('offline')
        to the frontend for all connected clients.
    """
    if current_user.is_authenticated:
        # Update user's status to 'offline' and set the 'last_seen' timestamp
        current_user.status = 'offline'
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

        # Retrieve all conversations the user is part of
        conversations = Conversation.query.filter(
            (Conversation.user1_id == current_user.id) |
            (Conversation.user2_id == current_user.id)
        ).all()

        # Iterate through each conversation the user is part of
        for conversation in conversations:
            # Leave the conversation room using the conversation ID
            leave_room(f'conversation_{conversation.id}')

        # Emit status update to the frontend for all connected clients
        emit('status_update',
             {'user_id': current_user.id, 'status': 'offline'},
             room=current_user.id)


@socketio.on('status_update')
def handle_status_update(data):
    user_id = data.get('user_id')
    status = data.get('status')
    emit('status_update', {'user_id': user_id,
         'status': status}, broadcast=True)


@socketio.on('send_message')
def handle_send_message(data):
    try:
        conversation_id = data['conversation_id']
        sender_id = data['sender_id']
        message_content = data['message']
        timestamp = datetime.now(pytz.utc)

        # Get the conversation from the database
        conversation = Conversation.query.filter_by(id=conversation_id).first()

        if conversation:
            last_message_date = datetime.now(pytz.utc)

            # For group conversations, there is no specific receiver_id
            receiver_id = None if conversation.type == 'group' else data.get(
                'receiver_id')

            # Create a new message and add it to the database
            new_message = Message(
                conversation_id=conversation_id,
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=message_content,
                timestamp=timestamp
            )
            timestamp_str = timestamp.isoformat()
            db.session.add(new_message)

            # Update the conversation's last message and last message date
            conversation.last_message = message_content
            conversation.last_message_date = last_message_date
            db.session.commit()

            # Emit the message with the formatted timestamp
            emit('new_message', {
                'conversation_id': conversation_id,
                'sender_id': sender_id,
                'message': message_content,
                'timestamp': timestamp_str,
                # Use isoformat for a standard timestamp
                'last_message_date': last_message_date.isoformat()
            }, room=f'conversation_{conversation_id}')

            # Emit last message update to all users listening
            emit('last_message_update', {
                'conversation_id': conversation_id,
                'last_message': message_content,
                'last_message_date': last_message_date.isoformat()
            }, broadcast=True)

            # Emit chat history update to the room
            emit('chat_history_update', {
                 'conversation_id': conversation_id},
                 room=f'conversation_{conversation_id}')
        else:
            emit('error', {'error': 'Conversation not found.'})

    except KeyError as e:
        print(f"Missing key: {e}")
        emit('error', {'error': f'Missing key: {e}'})
    except Exception as e:
        print(f"Error: {e}")
        emit('error', {'error': f'An error occurred: {e}'})


@socketio.on('send_group_message')
def handle_send_group_message(data):
    try:
        sender_id = data['sender_id']
        group_id = data['group_id']
        content = data['content']
        timestamp = datetime.now()
    except KeyError as e:
        print(f'Missing key: {str(e)}')  # Log which key is missing
        return {'error': f'Missing key: {str(e)}'}

    # Check if the group exists
    group = Group.query.get(group_id)
    if not group:
        return {"error": "Group not found"}

    # Find or create a conversation for the group
    conversation = Conversation.query.filter_by(group_id=group.id).first()
    if not conversation:
        conversation = group.create_group_conversation()

    sender = User.query.get(sender_id)
    if not sender:
        return {"error": "Sender not found"}
    sender_name = sender.name
    # Create the message
    message = Message(
        content=content,
        sender_id=sender_id,
        group_id=group_id,
        conversation_id=conversation.id,
        timestamp=datetime.now(pytz.utc)
    )
    timestamp_str = timestamp.isoformat()

    db.session.add(message)
    db.session.commit()

    # Emit the message to the group room
    emit('new_group_message', {
        'sender_id': sender_id,
        'sender_name': sender_name,
        'group_id': group_id,
        'content': content,
        'timestamp': timestamp_str,
        'message_id': message.id,
        'conversation_id': conversation.id
    }, room=f'group_{group.id}')
    # Emit group history update
    emit('group_history_update', {
        'group_id': group.id,
        'conversation_id': conversation.id
    }, room=f'group_{group.id}')
    return {"success": "Message sent successfully"}
