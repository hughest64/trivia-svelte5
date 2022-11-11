import type { RequestHandler } from './$types';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

export const GET: RequestHandler = async ({ params }) => {
    const apiResponse = await fetch(`${apiHost}/game/${params.joincode}`);
    const resp = new Response(apiResponse.body);
    return resp;
};