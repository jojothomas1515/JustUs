interface User {

    id: string,
    first_name: string,
    last_name: string,
    middle_name: string,
    email: string,
    date_of_birth: string | null
}

interface Friend {
    status: string,
    requester_id: string,
    data: User,
}


interface Mesg {
    id: string,
    message: string,
    receiver_id: string,
    sender_id: string,
    timestamp: string
}

interface Users {
    data: User,
    status: string
}

interface ReceivedMessage {
    message: string,
    timestamp: string | null,
    sender: User
}