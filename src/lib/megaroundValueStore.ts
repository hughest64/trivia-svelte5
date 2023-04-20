import { writable, type Writable } from 'svelte/store';
import type { Response } from './types';

export interface MegaRoundValue {
    num: string;
    used: boolean;
}

export interface MegaRoundValueStore extends Writable<MegaRoundValue[]> {
    reset: () => void;
    markUsed: (num: string, resetNum?: string) => void;
    getValue: (num: string) => MegaRoundValue | undefined;
}

export const defaultMegaroundValues: MegaRoundValue[] = [
    { num: '1', used: false },
    { num: '2', used: false },
    { num: '3', used: false },
    { num: '4', used: false },
    { num: '5', used: false }
];

export const getMegaroundValues = (responses: Response[]): MegaRoundValue[] => {
    return [1, 2, 3, 4, 5].map((num) => {
        const used = !!responses.find((resp) => resp.megaround_value === num);
        return { num: String(num), used };
    }) as MegaRoundValue[];
};

export const megaRoundValueStore = (initial?: MegaRoundValue[]): MegaRoundValueStore => {
    // TODO: validate that this is enough to not modify the global!
    const internalValues = initial || [...defaultMegaroundValues];
    const { subscribe, set, update } = writable(internalValues);

    return {
        subscribe,
        set,
        update,
        getValue: (num) => internalValues.find((val) => val.num === num),
        reset: () =>
            update((current) => {
                const newValues = [...current];
                for (const val of newValues) {
                    val.used = false;
                }
                return newValues;
            }),
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
