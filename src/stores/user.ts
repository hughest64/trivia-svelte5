import { derived, writable } from "svelte/store";
import type { Writable } from "svelte/store"

export interface UserData {
    username?: string;
    email?: string;
    is_staff?: string;
    active_team_id?: string | number;
    user_is_anonymous?: boolean;
    user_home_locations?: string[] // This might be it's own type?
}

// set active team id on the user model and include here
export const userdata: Writable<UserData> = writable({});

export interface TeamMember {
    username: string;
}
export interface UserTeam {
    team_id: string | number;
    team_name: string;
    // TODO: we've updated this to password when it's visible, but the field is still join_code
    join_code: string;
    team_members?: TeamMember[];
}
export const userteams: Writable<UserTeam[]> = writable([]);

export const useractiveteam = derived(
    [userdata, userteams],
    ([$userdata, $userteams]) => {
        // TODO: we could probably even get this to set in session storage
        return $userteams.find((team) => team.team_id === $userdata.active_team_id) || ''
})