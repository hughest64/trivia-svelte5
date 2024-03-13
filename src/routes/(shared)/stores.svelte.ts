import { getContext, setContext } from 'svelte';
import type { UserData, UserTeam } from '$lib/types';

export class UserState implements UserData {
    id;
    username;
    is_staff;
    is_guest;
    auto_reveal_questions;
    email;
    active_team_id;
    active_team;
    teams;
    user_is_anonymous;
    home_location;

    constructor(userData: UserData) {
        this.id = $state(userData.id);
        this.username = userData.username;
        this.is_staff = userData.is_staff;
        this.is_guest = userData.is_guest;
        this.auto_reveal_questions = $state(userData.auto_reveal_questions);
        this.email = $state(userData.email);
        this.active_team_id = $state(userData.active_team_id);
        this.active_team = $state(userData.active_team);
        this.teams = $state(userData.teams);
        this.user_is_anonymous = $state(userData.user_is_anonymous);
        this.home_location = $state(userData.home_location);
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
