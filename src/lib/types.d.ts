/* eslint-disable @typescript-eslint/no-explicit-any*/

import type { ServerLoadEvent } from '@sveltejs/kit';
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

export interface LeaderboardEntry {
    team_id: number;
    team_name: string;
    rank?: number;
    total_points: number;
}

export interface PublicLeaderboard {
    through_round?: number;
    leaderboard_entries: LeaderboardEntry[];
}

// TODO
// export interface HostLeaderboard extends PublicLeaderboard {
//     //
// }

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
    joincode: string | number;
    // reveal_answers: boolean;
    current_round_number: number;
    current_question_number: number;
}

export type PlayerJoined = boolean;

export interface CurrentEventData {
    round_number: number;
    question_number: number;
    question_key: key;
}

export interface Response {
    id: number;
    recorded_answer: string;
    points_awarded: number;
    funny: boolean;
    locked: boolean;
    round_number: string | number;
    question_number: string | number;
    key: string;
}

export interface HostResponse extends Omit<Response, ['id', 'locked']> {
    response_ids: number[];
    fuzz_ratio?: number;
}

export interface PopupData {
    is_displayed: boolean;
    popup_type: string;
    timer_value?: number;
    title?: string;
    message?: string;
    data?: Record<string, any>;
    anchor?: string;
}

export interface ActiveEventData {
    activeRoundNumber: number;
    activeQuestionNumber: number;
    activeQuestionKey: string;
}

export interface SocketMessage {
    msg_type: string;
    message: any;
}

export interface StoreTypes {
    userData: Writable<UserData>;
    eventData: Writable<EventData>; // Readable?
    activeEventData: Writable<ActiveEventData>;
    currentEventData: Writable<CurrentEventData>;
    rounds: Writable<GameRound[]>;
    questions: Writable<GameQuestion[]>; // Readable?
    roundStates: Writable<RoundState[]>;
    questionStates: Writable<QuestionState[]>;
    responseData: Writable<Response[]>;
    hostResponseData: Writable<HostResponse[]>;
    popupData: Writable<PopupData>;
    // eventPageData: unknown; // this is not used?
    publicLeaderboard: Writable<PublicLeaderboard>;
    playerJoined: Writable<boolean>;
}

export type MessageHandler = Record<string, (message: any) => unknown>;

interface CustomLoadEvent extends ServerLoadEvent {
    endPoint?: string;
}
