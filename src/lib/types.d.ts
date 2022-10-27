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
    validtoken?: boolean
}

export interface UserData {
    id: number;
    username: string;
    is_staff: boolean;
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

export interface EventQuestion {
    id: string | number;
    text: string;
    answer: string;
    question_number: number;
    key: string;
    question_type: string;
    question_url: string;
    question_displayed: boolean;
    answer_displayed: boolean;
}

export interface EventRound {
    id: string | number;
    title: string;
    description: string;
    round_number: number;
    locked: boolean;
    scored: boolean;
    questions: EventQuestion[];
}

export interface EventData {
    event_id: string | number;
    game_id: string | number;
    game_title: string;
    location: string;
    join_code: string | number;
    rounds: EventRound[];
    reveal_answers: boolean;
    current_round_number: number;
    current_question_number: number;
}

// TODO: many more fields to add here
export interface Response {
    id: number;
    recorded_answer: string;
    round_number: string | number;
    question_number: string | number;
    key: string // `${round_number}.${question_number}
}

export interface ActiveEventData {
    activeRoundNumber: number;
    activeQuestionNumber: number;
}

export type AllStores = EventData | ActiveEventData | EventQuestion | EventRound | UserData | Response[];

export interface SocketMessage {
    type: string;
    store: StoreKey;
    message: AllStores
}

export type StoreKey = 'userData' | 'eventData' | 'activeEventData' | 'responseData';
export type StoreType = Writable<AllStores>;
export type StoreMap = Map<StoreKey, StoreType>

// export type MessageHandler = Record<
//     string,
//     (message: SocketMessage['message'], store: StoreType) => unknown
// >;
