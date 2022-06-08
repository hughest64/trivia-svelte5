// import { writable, type Writable } from "svelte/store";

export interface LocationSelectData {
    location_id: string | number;
    locaiotn_name: string;
}

export interface EventSelectData {
    game_id: string | number;
    game_title: string;
}

export interface HostSelectData {
    event_select_data?: EventSelectData[];
    location_select_data?: LocationSelectData[];
}

// export const locationSelectData: Writable<LocationSelectData[]> = writable([]);
// export const eventSelectData: Writable<EventSelectData[]> = writable([]);
