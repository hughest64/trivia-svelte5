import { writable } from "svelte/store";
import type { Writable } from "svelte/store"

// TODO:
// make this an object like teamData = { teams: [], activeTeam: '2' }
export let teams: Writable<string[]> = writable([]);