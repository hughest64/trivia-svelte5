import type { LocationSelectData, UserData, UserTeam } from '$lib/types';

export class UserState {
    id;
    username;
    is_staff;
    is_guest;
    auto_reveal_questions = $state<boolean>();
    email = $state<string>();
    active_team_id = $state<number | null>();
    teams = $state<UserTeam[]>([]);
    active_team = $derived<UserTeam | undefined>(this.teams?.find((team) => team.id === this.active_team_id));
    user_is_anonymous = $state<boolean>();
    home_location = $state<LocationSelectData>();

    constructor(userData: UserData) {
        this.id = userData.id;
        this.username = userData.username;
        this.is_staff = userData.is_staff;
        this.is_guest = userData.is_guest;
        this.auto_reveal_questions = userData.auto_reveal_questions;
        this.email = userData.email;
        this.active_team_id = userData.active_team_id;
        this.teams = userData.teams;
        this.user_is_anonymous = userData.user_is_anonymous;
        this.home_location = userData.home_location;
    }
}
