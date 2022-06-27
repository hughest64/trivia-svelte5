import type { RequestHandler } from "@sveltejs/kit";
const apiHost = import.meta.env.VITE_API_HOST

// TODO: this probably needs to move client side as
// we aren't actually removing the token any more

export const get:RequestHandler = async() => {
    await fetch(
        `${apiHost}/user/logout/`,
        {
            method: "POST",
            credentials: 'include'
        }
    )

    return {
        status: 302,
        headers: {
            accept: 'application/json',
            location: '/user/login'
        }
    }
}