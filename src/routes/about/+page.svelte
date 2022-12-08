<script lang="ts">
    const anchorText = 'Take me to Login';
</script>

<svelte:head><title>Trivia Mafia | About</title></svelte:head>

<div class="container">
    <h1>About the Demo</h1>
    <hr>
    <a href="/">{anchorText}</a>
    <h3>Some things you can do in this demo:</h3>
    <ul>
        <li>
            <p>- Login via the login form (if you have an account in the demo)</p>
        </li>
        <li>
            <p>- Play as a guest (though it's a single user called "guest", so everyone shares it</p>
        </li>
        <li>
            <p>- Navigate event 1234</p>
        </li>
        <li>
            <p>- Answer questions (though you'll be guessing in the image round)</p>
        </li>
        <li>
            <p>- Host a game (if you are a staff member)</p>
        </li>
        <li>
            <p>- Reveal questions (as a host)</p>
        </li>
        <li>
            <p>- Lock rounds (as a host)</p>
        </li>
    </ul>

    <h3>Some things you cannot do:</h3>
    <ul>
        <li>
            <p>- Create a user - though if you an account in the demo you can login</p>
        </li>
        <li>
            <p>- Create a team - though you can play with one of several (poorly named) pre-existing teams</p>
        </li>
        <li>
            <p>- Join a team via password</p>
        </li>
        <li>
            <p>- Login with Google or Github</p>
        </li>
        <li>
            <p>
                - Use a join code other than <span style="font-weight: bold;">1234</span> (anything else will net you a
                <span style="font-weight: bold;">404</span>)
            </p>
        </li>
        <li>
            <p>- Record Answer Notes</p>
        </li>
    </ul>

    <h3>Some obvious missing features:</h3>
    <ul>
        <li>
            <p>- Megarounds</p>
        </li>
        <li>
            <p>- Scoring</p>
        </li>
        <li>
            <p>- Leaderboards</p>
        </li>
        <li>
            <p>- Chat</p>
        </li>
        <li>
            <p>- Private Events</p>
        </li>
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
            margin: .75em 0;
            font-weight: bold;
            color: var(--color-red);
        }
        ul {
            margin-bottom: 3em;
        }
        li {
            margin: .5em 0;
        };
    }
    @media (max-width: 1000px) {
        .container {
            margin: 0 1.5em;
        }
    }
</style>
