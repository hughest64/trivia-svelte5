import { derived, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store"

// TODO: teams as part of UserData

export interface UserData {
    username: string;
    is_staff: string;
    email?: string;
    active_team_id?: string | number;
    user_is_anonymous?: boolean;
    user_home_locations: string[] // This might be it's own type?
}

// set active team id on the user model and include here
export const userdata: Writable<UserData> = writable();

export interface UserTeam {
    team_id: string | number;
    team_name: string;
    // TODO: we've updated this to password when it's visible, but the field is still join_code
    join_code: string;
    team_members?: string[];
}
export const userteams: Writable<UserTeam[]> = writable([]);

export const useractiveteam: Readable<UserTeam | undefined> = derived(
    [userdata, userteams],
    ([$userdata, $userteams]) => {
        return $userteams.find((team) => team.team_id === $userdata.active_team_id)
})