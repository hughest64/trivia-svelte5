<script lang="ts">
    let errorMessage: string;
    let username: string;
    let password: string;

    const validateUser = () => {

    }
</script>

<h1>Login Why Doncha'</h1>

<form on:submit|preventDefault={validateUser}>
    {#if errorMessage}<h3>{errorMessage}</h3>{/if}
    <label for="username">Username:</label>
    <input type="text" id="username" bind:value={username}>
    <label for="password">Password:</label>
    <input type="password" id="password" bind:value={password}>
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