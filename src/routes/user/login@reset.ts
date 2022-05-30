export async function post({ request }) {
    const form = await request.formData()
    const response = await fetch(
        'http://localhost:8000/user/login/',
        {
            method: "POST",
            headers: {'content-type': 'application/json'},
            body: JSON.stringify({
                username: form.get('username'),
                password: form.get('password')
            })
        }
    )
    console.log(response)
    return {
        status: 303,
        headers: {
            location: '/'
        },
    }
}