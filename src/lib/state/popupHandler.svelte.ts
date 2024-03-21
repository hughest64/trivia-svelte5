import type { PopupData } from "$lib/types";

export class PopupHandler {
    is_displayed? = $state(false);
    // TODO: s5 - perhaps specific values for the type here?
    popup_type = $state<string>();
    timer_value = $state<number>();
    title = $state<string>();
    message = $state<string>();
    data = $state<Record<string, any>>();
    anchor = $state<string>();

    constructor(data: Partial<PopupData>) {
        this.is_displayed = data.is_displayed;
        this.timer_value = data.timer_value;
        this.title = data.title;
        this.message = data.message;
        this.data = data.data;
        this.anchor = data.anchor;
    }
}