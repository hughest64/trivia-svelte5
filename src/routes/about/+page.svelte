<script lang="ts">
    const anchorText = 'Take me to Login';
</script>

<svelte:head><title>Trivia Mafia | About</title></svelte:head>

<div class="container">
    <h1>About the Demo</h1>
    <hr />
    <a href="/">{anchorText}</a>
    <h3>Some things you can do in this demo:</h3>
    <ul>
        <li>- Create a user</li>
        <li>- Login via the login form</li>
        <li>- Play as a guest (though it's a single user called "guest", so everyone shares it</li>
        <li>- Create a team</li>
        <li>- Join a team via password</li>
        <li>- Join event 1234</li>
        <li>- Navigate event 1234</li>
        <li>- Answer questions (though you'll be guessing in the image round)</li>
        <li>- View the public leaderboard (though it does not yet show rank or points)</li>
        <li>- Host a game (if you are a staff member)</li>
        <li>- Reveal questions (as a host)</li>
        <li>- Lock rounds (as a host)</li>
        <li>- Score responses (as a host)</li>
    </ul>

    <h3>Some things you cannot do:</h3>
    <ul>
        <li>- Login with Google or Github</li>
        <li>- Create events</li>
        <li>
            - Use a join code other than <span style="font-weight: bold;">1234</span> (anything else will net you a
            <span style="font-weight: bold;">404</span>)
        </li>
        <li>
            - Well, technically event <span style="font-weight: bold;">9998</span> is playable, but consider it reserved
            for load testing responses
        </li>
        <li>- Record Answer Notes</li>
    </ul>

    <h3>Some obvious missing features:</h3>
    <ul>
        <li>- Megarounds</li>
        <li>- Chat</li>
        <li>- Private Events</li>
        <li>- Airtable Imports (this works via the command line but not in the admin)</li>
    </ul>
    <a href="/">{anchorText}</a>
</div>

<style lang="scss">
    .container {
        align-items: flex-start;
        margin: 0 20%;
        padding: 1.5em 0;
        h1 {
            font-size: 2.5em;
        }
        hr {
            margin-bottom: 3em;
            height: 3px;
            background-color: var(--color-black);
        }
        h3 {
            margin: 0.75em 0;
            font-weight: bold;
            color: var(--color-red);
        }
        ul {
            margin-bottom: 3em;
        }
        li {
            margin: 0.5em 0;
        }
    }
    @media (max-width: 1000px) {
        .container {
            margin: 0 1.5em;
        }
    }
</style>
