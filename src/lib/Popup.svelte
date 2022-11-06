<script lang="ts">
    import '$lib/styles/popup.scss';
</script>

<div class="pop">
    <div class="pop-timer">
        <!-- if there is a counter -->
        <h4>5</h4>
        <!-- <div> -->
            <!-- svg.pop-timer-svg > g.pop-timer-circle > circle.pop-timer-path-elapsed + path#pop-timer-path-remaining -->
            <!-- <span class="counter-value">5</span> -->
        <!-- </div> -->
    </div>
    <div class="pop-content">
        <!-- <h4>Title</h4> -->
        <!-- <h4>Message - Bold</h4> -->
        <p>The Next Question Will Be Revealed in 5 seconds</p>
        <!-- button for cases that require use interaction -->
    </div>
    <button class="dismiss" on:click>X</button>
</div>
