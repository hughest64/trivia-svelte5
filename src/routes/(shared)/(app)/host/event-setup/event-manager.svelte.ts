import type { GameSelectData, LocationSelectData, TodaysEventsData } from '$lib/types';

export interface EventSetupData
    extends Pick<App.PageData, 'game_select_data' | 'location_select_data' | 'game_block_data' | 'todays_events'> {}

const BLOCK_LETTERS = ['a', 'b', 'c', 'd'];

export class EventSetupManager {
    game_select_data = $state<GameSelectData[]>([]);
    game_block_data = $state<string[]>([]);
    location_select_data = $state<LocationSelectData[]>([]);
    todays_events = $state<TodaysEventsData[]>([]);

    selectedLocation = $state(this.location_select_data[0]);
    useSound = $state<boolean>(this.selectedLocation?.use_sound || true);
    playerLimit = $state(false);
    useThemeNight = $state(false);

    visbleBlocks = $state<string[]>([]);

    selectedBlock = $state(this.visbleBlocks[0]);
    selectedGame = $derived(
        this.game_select_data.filter((g) => g.block === this.selectedBlock && g.use_sound === this.useSound)[0]
    );
    selectedEventExists = $derived(
        !!this.todays_events.find(
            (e) => e.location_id === this.selectedLocation?.location_id && e.game_id === this.selectedGame?.game_id
        )
    );

    constructor(data: EventSetupData) {
        this.game_select_data = data.game_select_data || [];
        this.game_block_data = data.game_block_data?.sort() || [];
        this.location_select_data = data.location_select_data || [];
        this.todays_events = data.todays_events || [];
        this.setVisiblBlocks();
    }

    setVisiblBlocks() {
        if (!this.useThemeNight) {
            this.visbleBlocks = this.game_block_data?.filter((b) => BLOCK_LETTERS.includes(b.toLocaleLowerCase()));
        } else {
            this.visbleBlocks = this.game_block_data?.filter((b) => !BLOCK_LETTERS.includes(b.toLocaleLowerCase()));
        }
    }

    toggleUseSound() {
        this.useSound = !this.useSound;
    }

    toggleUseThemeNight() {
        this.useThemeNight = !this.useThemeNight;
        this.setVisiblBlocks();
    }

    togglePlayerLimit() {
        this.playerLimit = !this.playerLimit;
    }
}
