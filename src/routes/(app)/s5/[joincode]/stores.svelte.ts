import type { QuestionState, RoundState, CurrentEventData } from '$lib/types';

export class GameState {
    current_event_data?: CurrentEventData = $state({} as CurrentEventData);
    round_states: RoundState[] = $state([]);
    question_states?: QuestionState[] = $state([]);

    locked_rounds: number[] = $derived(this.round_states?.filter((rs) => rs.locked).map((rs) => rs.round_number));
    max_locked_round: number = $derived(Math.max(...this.locked_rounds) || 0);

    constructor(round_states: RoundState[], question_states?: QuestionState[], current_event_data?: CurrentEventData) {
        this.current_event_data = current_event_data;
        this.round_states = round_states;
        this.question_states = question_states;
    }

    updateRoundStates(roundState: RoundState) {
        const rsIndex = this.round_states.findIndex((rs) => rs.round_number === roundState.round_number);

        rsIndex > -1 && (this.round_states[rsIndex].locked = true);
    }
}
