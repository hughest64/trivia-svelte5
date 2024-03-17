import type {ActiveEventData, CurrentEventData } from '$lib/types'

// TODO: s5 - make keys of current and active event data more consistent
export class EventHandler {
    event_data
    rounds
    questions
    currentEventData
    activeEventData

    constructor(data: App.PageData & App.Locals) {
        this.event_data = data.event_data;
        this.rounds = data.rounds
        this.questions = data.questions

        // TODO: s5 - ick
        this.currentEventData = this.setCurrentEventData(
            Number(data.current_event_data?.question_number),
            Number(data.current_event_data?.round_number),
            // data.current_event_data?.question_key
        )
        this.activeEventData = this.setActiveEventData(
            Number(data.activeQuestionNumber), Number(data.activeRoundNumber)
        )
    }

    setCurrentEventData(question: number, round: number, key?: string,): CurrentEventData {
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