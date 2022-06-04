
// keeping this for posterity, may revert to it at some point

import * as cookie from 'cookie';
// import type { RequestHandler } from "./__types/login@reset2"

// export const get: RequestHandler = async({ request }) => {
    
//     const response = await fetch(
//         'http://localhost:8000/user/login/',
//         {
//             headers: {
//                 accept: 'application/json',
//             },
//             credentials: 'include'
//         }
//     )
//     if (response.ok) {
//         const csrfTokenCookie = cookie.parse(
//             <string>response.headers.get('set-cookie')
//         ) || {}

//         return {
//             status: 200,
//             body: {
//                 csrftoken: csrfTokenCookie['csrftoken']
//             }
//         }

//     }
//     return {
//         response: 200
//     }
// }

// export const post: RequestHandler = async(event) => {
//     const form = await event.request.formData()
//     const csrfToken = <string>form.get('csrftoken') || ''

//     const response = await fetch(
//         'http://localhost:8000/user/login/',
//         {
//             method: "POST",
//             headers: {
//                 'content-type': 'application/json',
//                 'Cookie': `csrftoken=${csrfToken}`,
//                 'X-CSRFToken': csrfToken,
//                 mode: 'same-origin'
//             },
//             body: JSON.stringify({
//                 username: form.get('username'),
//                 password: form.get('password')
//             }),
//             credentials: 'include'
//         }
//     )
//     console.log(response)
//     const cook = cookie.parse(
//         <string>response.headers.get('set-cookie')
//     )
//     console.log(cook)
//     return {
//         // status: 200
//         headers: {
//             'set-cookie': `jwt=${cook['jwt']}`,
//             location: '/'
//         },
//         status: 302,
//     }
// }