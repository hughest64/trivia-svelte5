import { derived, writable } from 'svelte/store';
import type { Readable, Writable } from 'svelte/store';

export interface UserData {
    username: string;
    is_staff: string;
    email?: string;
    active_team_id?: number | null;
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

export const userdata: Writable<UserData> = writable();

export const useractiveteam: Readable<UserTeam | undefined> = derived(userdata, ($userdata) => 
    $userdata.teams.find((team) => team.id === $userdata.active_team_id)
);
