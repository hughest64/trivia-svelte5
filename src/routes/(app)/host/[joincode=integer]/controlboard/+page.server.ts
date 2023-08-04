import { PUBLIC_API_HOST } from '$env/static/public';
import type { PageServerLoad } from './$types.js';

export const load: PageServerLoad = async ({ locals, params, fetch }) => {
    let apiData = {};

    const response = await fetch(`${PUBLIC_API_HOST}/host/${params.joincode}/tiebreaker`);
    if (response.ok) {
        apiData = await response.json();
    } else {
        // TODO: throw error
    }

    return { ...locals, ...apiData };
};

interface TiebreakerBody {
    tied_for_rank: FormDataEntryValue;
    question_id: FormDataEntryValue;
    team_data: Array<Record<string, FormDataEntryValue>>;
}

export const actions = {
    submit_tiebreakers: async ({ request, params, fetch }) => {
        const data = Object.fromEntries(await request.formData());
        const { tied_for_rank, question_id, ...teams } = data;
        const body: TiebreakerBody = { tied_for_rank, question_id, team_data: [] };

        for (const [team, answer] of Object.entries(teams)) {
            const team_id = team.split('.')[1];
            body.team_data.push({ team_id, answer });
        }

        const response = await fetch(`${PUBLIC_API_HOST}/host/${params.joincode}/tiebreaker`, {
            method: 'post',
            body: JSON.stringify(body)
        });

        const updateData = await response.json();
        console.log(updateData);

        if (!response.ok) {
            const responseData = await response.json();
            // TODO: error handling
        }

        return { success: true };
    }
};
