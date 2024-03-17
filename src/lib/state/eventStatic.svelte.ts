import type {ActiveEventData, CurrentEventData, RoundState, QuestionState } from '$lib/types'

// TODO: s5 - make keys of current and active event data more consistent
export class EventHandler {
    // static data
    event_data
    rounds
    questions

    // data that will change over time
    round_states= $state<RoundState[]>([]);
    question_states = $state<QuestionState[]>([]);
    currentEventData = $state<CurrentEventData>()
    activeEventData = $state<ActiveEventData>()

    // data derived from data that will change over time
    locked_rounds = $derived(this.round_states?.filter((rs) => rs.locked).map((rs) => rs.round_number));
    max_locked_round = $derived(Math.max(...this.locked_rounds) || 0);

    constructor(data: App.PageData & App.Locals) {
        this.event_data = data.event_data;
        this.rounds = data.rounds
        this.questions = data.questions

        this.round_states = data.round_states || [];
        this.question_states = data.question_states || [];
        this.currentEventData = this.setCurrentEventData(
            Number(data.current_event_data?.question_number),
            Number(data.current_event_data?.round_number),
        )
        this.activeEventData = this.setActiveEventData(
            Number(data.activeQuestionNumber), Number(data.activeRoundNumber)
        )
    }

    setCurrentEventData(question: number, round: number, key?: string): CurrentEventData {
        return  {
            round_number: round,
            question_number: question,
            question_key: key || `${round}.${question}`
        }
    }

    // TODO: s5 - this should use currentEventData as the first fallback
    setActiveEventData(question?: number, round?: number, key?: string, setCookie=false): ActiveEventData {
        const activeEventData = {
            activeQuestionNumber: question || 1,
            activeRoundNumber: round || 1,
            activeQuestionKey: key || `${round}.${key}`
        }
        // TODO: s5 if setCookie, do the thing
        return activeEventData
    }
}