import type { GameSelectData, LocationSelectData, TodaysEventsData, GameBlockData } from '$lib/types';

export interface EventSetupData
    extends Pick<App.PageData, 'game_select_data' | 'location_select_data' | 'game_block_data' | 'todays_events'> {}

const BLOCK_LETTERS = ['a', 'b', 'c', 'd'];

export class EventSetupManager {
    game_select_data = $state<GameSelectData[]>([]);
    game_block_data = $state<GameBlockData[]>([]);
    location_select_data = $state<LocationSelectData[]>([]);
    todays_events = $state<TodaysEventsData[]>([]);

    selectedLocation = $state<LocationSelectData>();
    useSound = $state<boolean>();
    playerLimit = $state(false);
    useThemeNight = $state(false);

    visibleBlocks = $state<string[]>([]);

    selectedBlock = $state<string>(this.visibleBlocks[0]);
    selectedGame = $state<GameSelectData>();

    selectedEventExists = $derived(
        !!this.todays_events.find(
            (e) => e.location_id === this.selectedLocation?.location_id && e.game_id === this.selectedGame?.game_id
        )
    );

    constructor(data: EventSetupData) {
        this.game_select_data = data.game_select_data || [];
        this.game_block_data = data.game_block_data || [];
        this.location_select_data = data.location_select_data || [];
        this.todays_events = data.todays_events || [];
        // set some things
        this.useSound = this.location_select_data[0].use_sound;
        this.setVisibleBlocks();
        this.setSelectedGame();
    }

    setVisibleBlocks() {
        const visbleBlockData = this.game_block_data?.filter((b) => {
            const show = b.is_theme_block === this.useThemeNight;
            return show;
        });
        this.visibleBlocks = visbleBlockData.map((b) => b.block).sort();
        this.selectedBlock = this.visibleBlocks[0];
    }

    setSelectedGame() {
        const game = this.game_select_data.filter(
            (g) => g.block === this.selectedBlock && g.use_sound === this.useSound
        )[0];
        this.selectedGame = game;
    }

    toggleUseSound() {
        this.useSound = !this.useSound;
        this.setSelectedGame();
    }

    toggleUseThemeNight() {
        this.useThemeNight = !this.useThemeNight;
        this.setVisibleBlocks();
        this.setSelectedGame();
    }

    togglePlayerLimit() {
        this.playerLimit = !this.playerLimit;
    }
}
