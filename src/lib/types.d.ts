/* eslint-disable @typescript-eslint/no-explicit-any*/

import type { ServerLoadEvent } from '@sveltejs/kit';
import type { Readable, Writable } from 'svelte/store';
import type { MegaRoundValueStore } from './megaroundValueStore';

export interface JwtPayload {
    // user.id
    id?: number;
    // user.is_staff
    staff_user?: boolean;
    // user.is_guest
    guest_user?: boolean;
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
    is_guest: boolean;
    auto_reveal_questions: boolean;
    email?: string;
    active_team_id?: number | null;
    active_team?: UserTeam | undefined;
    teams: UserTeam[];
    user_is_anonymous?: boolean;
    home_location?: LocationSelectData;
}
export interface UserTeam {
    id: string | number;
    name: string;
    password: string;
    members?: string[];
}

export interface ChatMessage {
    id: number;
    username: string;
    userid: number;
    team: string;
    team_id: number;
    is_host_message?: boolean;
    chat_message: string;
    time: string;
}

export interface LeaderboardEntry {
    id: number;
    team_id: number;
    team_name: string;
    rank?: number;
    tied_for_rank?: number;
    tiebreaker_round_number?: number;
    team_password?: string;
    megaround?: number;
    total_points: number;
    points_adjustment_value: number;
    points_adjustment_reason_id: number;
}

export interface HostMegaRoundInstance {
    team_id: number;
    has_megaround: boolean;
}

export interface Leaderboard {
    through_round?: number;
    synced?: boolean;
    public_leaderboard_entries: LeaderboardEntry[];
    host_leaderboard_entries?: LeaderboardEntry[];
    // array of objects with team id as a key and a boolean value
    // indicating whether or not they have selected a mega round
    host_megaround_list?: HostMegaRoundInstance[];
}
export interface LocationSelectData {
    location_id: string | number;
    location_name: string;
    use_sound: boolean;
}

export interface GameSelectData {
    game_id: string | number;
    game_title: string;
    block: string;
    use_sound: boolean;
}

export interface HostSelectData {
    game_select_data: GameSelectData[];
    location_select_data: LocationSelectData[];
}

export interface GameQuestion {
    id: string | number;
    question_type: string;
    question_text: string;
    question_notes: string;
    question_url: string;
    display_answer: string;
    answer_notes: string;
    round_number: number;
    question_number: number;
    key: string;
}

export interface TeamNote {
    id: number;
    event_id: number;
    team_id: number;
    user: string;
    question_id: number;
    text: string;
    time: string;
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
    question_count: number;
}

export interface RoundState {
    round_number: number;
    locked: boolean;
    scored: boolean;
    revealed: boolean;
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
    megaround_value?: number;
    funny: boolean;
    locked: boolean;
    round_number: string | number;
    question_number: string | number;
    key: string;
}

export interface TiebreakerResponse extends Pick<Response, 'recorded_answer' | 'round_number' | 'id'> {
    game_question_id: number;
    team_id: number;
    grade: number | string;
}

export interface HostResponse extends Omit<Response, ['id', 'locked']> {
    response_ids: number[];
    fuzz_ratio?: number;
}

export interface ResponseMeta {
    key: string;
    recorded_answer: string;
    points_awarded: string | number;
}

export interface ResponseSummaryValues {
    correct: number;
    half: number;
    total: number;
}
export interface ResponseSummary {
    [k: string]: ResponseSummaryValues;
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

export interface PointsAdjustmentReson {
    id: string | number;
    text: string;
}

export interface SocketMessage {
    msg_type: string;
    message: any;
}

export interface StoreTypes {
    userData: Writable<UserData>;
    eventData: Readable<EventData>;
    activeEventData: Writable<ActiveEventData>;
    currentEventData: Writable<CurrentEventData>;
    rounds: Readable<GameRound[]>;
    questions: Readable<GameQuestion[]>;
    roundStates: Writable<RoundState[]>;
    questionStates: Writable<QuestionState[]>;
    responseData: Writable<Response[]>;
    tiebreakerResponses: Writable<TiebreakerResponse[]>;
    responseSummary: Writable<ResponseSummary>;
    hostResponseData: Writable<HostResponse[]>;
    popupData: Writable<PopupData>;
    leaderboard: Writable<Leaderboard>;
    playerJoined: Writable<PlayerJoined>;
    megaroundValues: MegaRoundValueStore;
    selectedMegaRound: Writable<number | undefined>;
    chatMessages: Writable<ChatMessage[]>;
    teamNotes: Writable<TeamNote[]>;
}

export type MessageHandler = Record<string, (message: any) => unknown>;

interface CustomLoadEvent extends ServerLoadEvent {
    endPoint?: string;
}
