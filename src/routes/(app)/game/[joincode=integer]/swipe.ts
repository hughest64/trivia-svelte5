/**
 * compare the x coordinate from mousedown and mouseup and fire the custom "swipe" event if the distance
 * traveled is greater than theshold.
 *
 * @param {HTMLElement} node html element that uses this function
 * @param {number} threshold distance in pixels from mouse down to mouse up required in order to fire the event
 * @returns {Object} object containing a destroy method which removes the event listeners from the node
 */
export const swipeQuestion = (node: HTMLElement, threshold = 10) => {
    let startPostion = -1;
    let endPostion = -1;

    const handleMousedown = (event: MouseEvent | TouchEvent) => {
        startPostion = (event as MouseEvent).clientX || (event as TouchEvent).touches[0].pageX;
    };
    const handleMouseup = (event: MouseEvent | TouchEvent) => {
        const target = <HTMLElement>event.target;

        if (node.contains(target) && startPostion > -1) {
            endPostion = (event as MouseEvent).clientX || (event as TouchEvent).changedTouches[0].pageX;

            const direction = endPostion < startPostion ? 'right' : 'left';
            const shouldDispatch = Math.abs(startPostion - endPostion) > threshold;

            shouldDispatch && node.dispatchEvent(new CustomEvent('swipe', { detail: { direction } }));
        }
    };

    node.addEventListener('mousedown', handleMousedown);
    node.addEventListener('mouseup', handleMouseup);

    node.addEventListener('touchstart', handleMousedown);
    node.addEventListener('touchend', handleMouseup);

    return {
        destroy() {
            node.removeEventListener('mousedown', handleMousedown);
            node.removeEventListener('mouseup', handleMouseup);

            node.removeEventListener('touchstart', handleMousedown);
            node.removeEventListener('touchend', handleMouseup);
        }
    };
};
