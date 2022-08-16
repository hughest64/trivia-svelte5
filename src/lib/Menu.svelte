<script>
</script>

<!-- TODO: conditional elements based on $userdata.is_staff -->
<ul>
    <!-- TODO: anchors -->
    <li>Rules and FAQ</li>
    <li>Manage Profile</li>
    <li>Manage Team</li>
    <li>Trivia Mafia Administration</li>
    <li>Show Me the Tiebreakers</li>
    <li>Submit App Feedback</li>
    <li>Trivia Mafia Host Feedback</li>
    <li><a rel="external" href="/user/logout">Logout</a></li>
    <h4 on:click>X</h4>
</ul>

<style lang="scss">
    ul {
        display: flex;
        flex-direction: column;
        height: 100%;
        margin: 1em;
        color: var(--color-white);
        font-weight: bold;
    }
    li {
        margin: 1em 0;
        &:last-of-type {
            flex-grow: 1;
        }
    }
    a {
        text-decoration: none;
        color: var(--color-white);
    }
    h4 {
        width: fit-content;
        text-align: right;
        align-self: flex-end;
        font-size: 2em;
        color: var(--color-white);
        margin-bottom: 1em;
        cursor: pointer;
    }
</style>
