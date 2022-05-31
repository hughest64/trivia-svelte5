<script lang="ts">
    let errorMessage: string;
    export let csrftoken: string;

    // const validateUser = async() => {
    //     const response = await fetch(
    //         'http://localhost:8000/user/login/',
    //         {
    //             method: 'POST',
    //             headers: {'content-type': 'application/json'},
    //             body: JSON.stringify({ username, password })
    //         }
    //     )
    //     if (response.ok) {
    //         // set store values for user
    //     }
    //     console.log(response)
    // }
</script>

<h1>Login Why Doncha'</h1>

<!-- <form on:submit|preventDefault={validateUser}> -->
<form action="/user/login" method="post" name="login">
    {#if errorMessage}<h3>{errorMessage}</h3>{/if}
    <input type="hidden" id="csrftoken" name="csrftoken" value={csrftoken}>
    <!-- option to pass a value from the page to the fetch request -->
    <!-- though, I'm leaning a lot harder to just using validateUser -->
    <!-- and having the token come from a load function -->
    <!-- <input type="hidden" id="next" name="next" value="/next/page"> -->

    <label for="username">Username:</label>
    <input type="text" id="username" name="username">

    <label for="password">Password:</label>
    <input type="password" id="password" name="password">

    <input type="submit" value="Log In!">
</form>

<style>
    form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: .75em;
        max-width: 20rem;
        margin: 5rem auto 0;
    }
</style>