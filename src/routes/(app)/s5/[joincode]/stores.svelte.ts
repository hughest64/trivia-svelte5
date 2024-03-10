import type { QuestionState, RoundState, CurrentEventData } from '$lib/types';

export class GameState {
    current_event_data?: CurrentEventData = $state({} as CurrentEventData);
    round_states?: RoundState[] = $state([]);
    question_states?: QuestionState[] = $state([]);

    constructor(round_states?: RoundState[], question_states?: QuestionState[], current_event_data?: CurrentEventData) {
        this.current_event_data = current_event_data;
        this.round_states = round_states;
        this.question_states = question_states;
    }
}
