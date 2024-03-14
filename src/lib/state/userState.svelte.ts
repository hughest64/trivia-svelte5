import type { LocationSelectData, UserData, UserTeam } from '$lib/types';

export class UserState {
    id;
    username;
    is_staff;
    is_guest;
    auto_reveal_questions?: Boolean = $state();
    email?: string = $state();
    active_team_id?: number | null = $state();
    teams?: UserTeam[] = $state([]);
    active_team?: UserTeam = $derived(this.teams?.find((team) => team.id === this.active_team_id));
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
        this.teams = userData.teams;
        this.user_is_anonymous = userData.user_is_anonymous;
        this.home_location = this.home_location;
    }
}
