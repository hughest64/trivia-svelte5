import { getContext, setContext } from 'svelte';
import type { LocationSelectData, UserData, UserTeam } from '$lib/types';

export class UserState {
    id;
    username;
    is_staff;
    is_guest;
    auto_reveal_questions?: Boolean = $state();
    email?: string = $state();
    active_team_id?: number | null = $state();
    active_team?: UserTeam = $state();
    teams;
    user_is_anonymous?: boolean = $state();
    home_location?: LocationSelectData = $state();

    constructor(userData: UserData) {
        this.id = userData.id;
        this.username = userData.username;
        this.is_staff = userData.is_staff;
        this.is_guest = userData.is_guest;
        this.auto_reveal_questions = userData.auto_reveal_questions;
        this.email = userData.email;
        this.active_team_id = userData.active_team_id;
        this.active_team = userData.active_team;
        this.teams = userData.teams;
        this.user_is_anonymous = userData.user_is_anonymous;
        this.home_location = this.home_location;
    }
}

const stateMap = {
    userState: (data?: UserData) => data && new UserState(data)
};

interface StateTypes {
    userState?: UserState;
}

interface DataTypes {
    userState?: UserData;
}

export function createState<K extends keyof typeof stateMap>(key: K, data: DataTypes[K]): StateTypes[K] {
    return setContext(key, stateMap[key](data));
}

export function getState<K extends keyof typeof stateMap>(key: K): StateTypes[K] {
    return getContext(key);
}
