<script lang="ts">
    import { browser } from '$app/environment';
    import { afterNavigate } from '$app/navigation';
    import { getStore } from './utils';

    const userData = getStore('userData');
    const userEmail = $userData.email;
    const feedbackLink = `https://docs.google.com/forms/d/e/1FAIpQLSeT5FX2OGycY0yDqjiwj8ItAFi8CE64GatBiO-lsYAz1hLguA/viewform?usp=pp_url&entry.1807181492=${userEmail}`;

    let prevRoute = (browser && sessionStorage.getItem('previous_round')) || '/team';

    afterNavigate(({ from, to }) => {
        const fromPath = from?.url.pathname as string;
        const toPath = to?.url.pathname as string;
        if (fromPath && fromPath !== toPath) {
            prevRoute = fromPath;
            sessionStorage.setItem('previous_round', fromPath);
        }
    });
    const clearStorage = () => sessionStorage.removeItem('previous_round');
</script>

<svelte:head><title>Trivia Mafia | Rules</title></svelte:head>

<main class="short">
    <h1>Trivia Mafia Rules, Links, FAQ</h1>
    <a href={prevRoute} class="button button-tertiary" on:click={clearStorage} data-sveltekit-reload>Go Back</a>

    <article>
        <h3>How to play:</h3>
        <p>
            Trivia Mafia is a team-based trivia game played live at bars, breweries, and restaurants, or virtually. A
            host reads the questions. Teams answer the questions. The team that does so most often is declared the
            winner.
        </p>
        <p>
            The game is played over eight rounds. All rounds contain five questions, except the image round, which has
            10. There are two general knowledge rounds. All other rounds have themes.
        </p>
        <p>
            Scores are tallied twice during the game: Once at halftime, after Round 4; and again at the end. After
            scores are tallied, the host reads the answers to the four-round half that has just been completed.
        </p>
        <p>
            Teams select one second-half round to be their "Mega Round." This allows them to earn extra points by
            weighting each answer within that round 1-5 points, using each number once. A Mega Round is worth 15 points.
            A perfect score at a Trivia Mafia game is 55 points.
        </p>
        <p>Prizes (gift cards to the host venue, usually) are awarded to the top teams.</p>
        <p>There are two cardinal rules at every Trivia Mafia event:</p>
        <ol>
            <li>Use Your Noodle, Not Your Google. That means no cheating on your phone.</li>
            <li>No shouting answers. That means no shouting answers.</li>
        </ol>
        <h3>Helpful Links:</h3>
        <p><a href="/user/settings" data-sveltekit-reload>Update your profile, change your password or username</a></p>
        <p><a href={feedbackLink} target="_blank" rel="noopener noreferrer">Submit App Feedback</a></p>

        <p>
            <a href="https://www.triviamafia.com/contact" target="_blank" rel="noopener noreferrer">
                Contact Trivia Mafia
            </a>
        </p>

        <h3>FAQ:</h3>
        <p><strong> How many people can play on a team? </strong></p>
        <p>
            As few as one, and as many as eight. You can actually go over eight if you like, but we dock one point for
            every player on your team beyond the eight-player maximum.
        </p>
        <p><strong> Tell me more about the Sound Round. </strong></p>
        <p>
            Roughly half of our venues utilize the Sound Round. In these venues, the Sound Round is Round 8. You will
            hear five audio clips (usually music, but not always), and you will be asked to identify something about it
            (usually the artist and the song title, but not always).
        </p>
        <p>
            Locations that don't use the Sound Round will play the List Round. This is a one-question round with five
            correct answers. You earn 1 point for each of the answers you can come up with.
        </p>
        <p><strong> How does the Mega Round work? </strong></p>
        <p>
            At the end of the game, teams select which second-half round they feel the most confident about (that's
            rounds 4-8). After they've selected one of those rounds to be their Mega Round, they assign a point value to
            each answer: "5" for the answer they feel the best about, "4" for their second-most-confident answer, all
            the way down to "1" (their least-confident answer). A perfect score on the Mega Round is 15 points.
        </p>

        <p><strong> Don't people just cheat on their phones? </strong></p>
        <p>
            Honestly, no. I mean, sure, some teams occasionally do cheat. But the vast majority of Trivia Mafia teams
            are made up of cool, fun, respectful people who love trivia and realize that cheating at bar trivia isn't
            cool, fun, or respectful.
        </p>
        <p><strong> Do I have to be really good at trivia to play? </strong></p>
        <p>
            No! We pride ourselves on writing questions that are always entertaining, no matter the difficulty level.
            While we strive for a nice balance throughout the night, we make sure that even the most challenging
            questions are guessable, so you've always got a chance. And even when you don't get a question right, it's
            still fun to learn something new!
        </p>
        <p>
            Trivia Mafia questions cater to a wide variety of players with broad interests, skills, and experiences. We
            feel that the best trivia nights are the ones where every player feels like they've contributed to their
            team, and we work hard to build those experiences into our games.
        </p>
        <p>
            Also: Many locations give away prizes for "Best Team Name" or "Most Middle Score," so you don't even need to
            be at the top of the scoreboard to win something!
        </p>
        <p><strong>Is the app giving you trouble?</strong></p>

        <p>We want to hear about what the problem is, so drop us a line on our Feedback Form so that we can fix it!</p>
    </article>

    <a href={prevRoute} class="button button-tertiary" on:click={clearStorage} data-sveltekit-reload>Go Back</a>

    <small>App created by <a href="https://codeofthenorth.com" target="_blank">Code of the North</a></small>
</main>
