<script>
    import '$lib/styles/app.scss';
    import { browser } from '$app/environment';

    browser &&
        console.log(
            `%c
  _____        __           ___  __  __         _  __         __  __ 
 / ___/__  ___/ /__   ___  / _/ / /_/ /  ___   / |/ /__  ____/ /_/ / 
/ /__/ _ \\/ _  / -_) / _ \\/ _/ / __/ _ \\/ -_) /    / _ \\/ __/ __/ _ \\
\\___/\\___/\\_,_/\\__/  \\___/_/   \\__/_//_/\\__/ /_/|_/\\___/_/  \\__/_//_/
                                                                     
https://codeofthenorth.com                                                                                                                                                                                                                                                                                                                                                                                                                                                
`,
            `
font-size: 9px;
font-weight: bold;
color: rgb(112,195,159);
`
        );
</script>

<slot />

<style lang="scss">
    :global(body) {
        position: relative;
        margin: 0;
        min-height: 100vh;
    }
</style>
