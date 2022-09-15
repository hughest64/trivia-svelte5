import { getContext, setContext } from 'svelte';
import { 
    // derived,
    writable } from 'svelte/store';
import type { 
    // Readable,
    Writable } from 'svelte/store';

export interface UserData {
    id: number;
    username: string;
    is_staff: boolean;
    email?: string;
    active_team_id?: number | null;
    active_team?: UserTeam | null;
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

// export const userdata: Writable<UserData> = writable();

// export const useractiveteam: Readable<UserTeam | undefined> = derived(userdata, ($userdata) => {
//     return $userdata?.teams?.find((team) => team.id === $userdata.active_team_id);
// });

enum StoreKeys {
    userData = 'userData'
}

export const setUserActiveTeam = (userData: UserData) => (
    userData.active_team = userData.teams.find((team) => team.id === userData.active_team_id)
);

export const createUserStore = (userData: UserData): void => {
    // add the active team to the userdata fr
    userData && setUserActiveTeam(userData);
    setContext(StoreKeys.userData, writable(userData));
};

export const getUserStore = (): Writable<UserData> => {
    return getContext(StoreKeys.userData);
};
