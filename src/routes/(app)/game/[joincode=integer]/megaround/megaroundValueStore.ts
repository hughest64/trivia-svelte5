import { writable, type Writable } from 'svelte/store';

export interface MegaroundValue {
    num: string;
    used: boolean;
}

export interface MegaRoundValueStore extends Writable<MegaroundValue[]> {
    reset: () => void;
    markUsed: (num: string, resetNum?: string) => void;
}

export const defaultMegaroundValues: MegaroundValue[] = [
    { num: '1', used: false },
    { num: '2', used: false },
    { num: '3', used: false },
    { num: '4', used: false },
    { num: '5', used: false }
];

export const megaRoundValueStore = (initial = defaultMegaroundValues): MegaRoundValueStore => {
    const { subscribe, set, update } = writable(initial);

    return {
        subscribe,
        set,
        update,
        reset: () => set(defaultMegaroundValues),
        markUsed: (num, resetNum) => {
            update((current) => {
                const newValues = [...current];
                const indexToMark = newValues.findIndex((val) => val.num === num);
                if (indexToMark > -1) newValues[indexToMark].used = true;
                if (resetNum) {
                    const indexToReset = newValues.findIndex((val) => val.num === resetNum);
                    if (indexToReset > -1) newValues[indexToReset].used = false;
                }

                return newValues;
            });
        }
    };
};
