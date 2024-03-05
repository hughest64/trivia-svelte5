<!-- https://www.youtube.com/watch?v=zwl3kZPZ8H8 see this at about 7:11 for the rotate bit -->
<!-- https://css-tricks.com/snippets/svg/curved-text-along-path/ curved text svg example -->
<!-- code pen -->
<script lang="ts">
    export let questionKey = '1.1';
    $: displayedText = 'Current Question ' + questionKey;
</script>

<div class="btn-ctr">
    <div class="circle">
        <!-- This would be the blimp SVG -->
        <div class="logo" />
        <div class="text">
            {#each displayedText as char, i}
                <span style:transform={'rotate(i * 5)deg'}>char</span>
            {/each}
        </div>
    </div>
</div>

<style lang="scss">
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    .btn-ctr {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .circle {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 200px;
        height: 200px;
        background-color: blue;
        border-radius: 50%;
    }
    // blimp image
    .logo {
        position: absolute;
        width: 150px;
        height: 15px;
        // background-color: url();
        // background-size: cover;
    }
    .text {
        position: absolute;
        width: 100%;
        height: 100%;
        // NOTE this requires each charater to be in it's own span that is rotated
        // like <span style="transform:rotate(i * 5)deg">l</span>
        // where if is the index of the letter in the og string
        span {
            position: absolute;
            left: 50%;
            transform-origin: 0 100px;
        }
    }
</style>
