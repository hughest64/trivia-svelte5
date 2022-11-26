import type { Writable } from 'svelte/store';

export interface JwtPayload {
    // user.id
    id?: number;
    // user.is_staff
    staff_user?: boolean;
    // expiration timestamp
    exp?: number;
    // created timestamp
    iat?: number;
    // token exists and is not expired
    validtoken?: boolean;
}

export interface UserData {
    id: number;
    username: string;
    is_staff: boolean;
    auto_reveal_questions: boolean;
    email?: string;
    active_team_id?: number | null;
    active_team?: UserTeam | undefined;
    teams: UserTeam[];
    user_is_anonymous?: boolean;
    user_home_locations?: string[];
}

export interface UserTeam {
    id: string | number;
    name: string;
    password: string;
    members?: string[];
}

export interface LocationSelectData {
    location_id: string | number;
    location_name: string;
}

export interface GameSelectData {
    game_id: string | number;
    game_title: string;
}

export interface HostSelectData {
    game_select_data: GameSelectData[];
    location_select_data: LocationSelectData[];
}

export interface GameQuestion {
    id: string | number;
    question_type: string;
    question_text: string;
    question_url: string;
    display_answer: string;
    answer_notes: string;
    round_number: number;
    question_number: number;
    key: string;
}

export interface QuestionState {
    round_number: number;
    question_number: number;
    key: string;
    question_displayed: boolean;
    answer_displayed: boolean;
}

export interface GameRound {
    id: string | number;
    title: string;
    round_description: string;
    round_number: number;
}

export interface RoundState {
    round_number: number;
    locked: boolean;
    scored: boolean;
}

export interface EventData {
    event_id: string | number;
    game_title: string;
    location: string;
    join_code: string | number;
    // reveal_answers: boolean;
    current_round_number: number;
    current_question_number: number;
}

export interface CurrentEventData {
    round_number: number;
    question_number: number;
    question_key: key;
}

// TODO: many more fields to add here
export interface Response {
    id: number;
    recorded_answer: string;
    round_number: string | number;
    question_number: string | number;
    key: string; // like: `${round_number}.${question_number}
}

export interface PopupData {
    is_displayed: boolean;
    popup_type: string; // TODO: specific types?
    timer_value?: number;
    title?: string;
    message?: string;
    /* eslint-disable-next-line @typescript-eslint/no-explicit-any*/
    data?: Record<string, any>;
    anchor?: string;
}

export interface ActiveEventData {
    activeRoundNumber: number;
    activeQuestionNumber: number;
    activeQuestionKey: string;
}

export interface EventPageData {
    roundNumbers: number[],
    activeRound?: GameRound,
    questionNumbers: number[],
    activeRoundState?: RoundState,
    activeQuestion?: GameQuestion,
    activeQuestionState?: QuestionState,
    activeResponse?: Response;
    activeRoundNumber: number;
    activeQuestionKey: string;
    currentRoundNumber: number;
    currentQuestionKey: string;
}

export type AllStores =
    | EventData
    | ActiveEventData
    | GameQuestion[]
    | GameRound[]
    | QuestionState[]
    | RoundState[]
    | UserData
    | Response[]
    | CurrentEventData
    | EventPageData

export interface SocketMessage {
    type: string;
    store: StoreKey;
    message: AllStores;
}

export type StoreKey =
    | 'userData'
    | 'eventData'
    | 'activeEventData'
    | 'currentEventData'
    | 'rounds'
    | 'questions'
    | 'roundStates'
    | 'questionStates'
    | 'responseData'
    | 'popupData'
    | 'eventPageData';

export type StoreType = Writable<AllStores>;
export type StoreMap = Map<StoreKey, StoreType>;

/* eslint-disable-next-line @typescript-eslint/no-explicit-any*/
export type MessageHandler = Record<string, (message: any, store: Writable<any>) => unknown>;
