import { writable } from "svelte/store";
import type { Writable } from "svelte/store"

export interface UserData {
    username?: string;
    email?: string;
    is_staff?: string;
}

export const userdata: Writable<UserData> = writable({});

// TODO:
// make this an object like teamData = { teams: [], activeTeam: '2' }
export const userteams: Writable<string[]> = writable([]);