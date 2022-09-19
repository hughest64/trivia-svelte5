interface EventData {
    event_id: string | number;
    game_id?: string | number;
    game_title: string;
    location: string;
    join_code: string | number;
    // rounds: EventRound[];
    reveal_answers: boolean;
    current_round_number: number;
    current_question_number: number;
    active_round_number?: number;
    active_question_number?: number;
}

export class EventDataTwo {
    event_id;
    // game_id: string | number;
    // game_title: string;
    // location: string;
    // join_code: string | number;
    // rounds: EventRound[];
    // reveal_answers: boolean;
    // current_round_number: number;
    // current_question_number: number;
    // active_round_number?: number;
    // active_question_number?: number;
    constructor(data: EventData) {
        this.event_id = data.event_id;
    }
}