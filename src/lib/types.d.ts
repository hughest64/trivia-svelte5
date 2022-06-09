export interface LocationSelectData {
    location_id: string | number;
    locaiotn_name: string;
}

export interface GameSelectData {
    game_id: string | number;
    game_title: string;
}

export interface HostSelectData {
    game_select_data?: GameSelectData[];
    location_select_data?: LocationSelectData[];
}