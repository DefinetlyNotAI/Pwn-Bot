const width = 500; // Width of our canvas
const height = 500; // Height of our canvas

setDocDimensions(width, height);

// Head
const headRadius = 20;
const headPosition = [width / 2, height * 0.75]; // Position the head towards the top center
drawLines(bt.circle(headPosition, headRadius));

// Torso
const torsoRadius = 40;
const torsoPosition = [width / 2, height * 0.5]; // Position the torso below the head
drawLines(bt.circle(torsoPosition, torsoRadius));

// Spine
drawLines([
    [[headPosition[0], headPosition[1] + headRadius], [torsoPosition[0], torsoPosition[1] - torsoRadius]]
]);

// Arms
const armLength = 100;
drawLines([
    [[headPosition[0] - armLength, headPosition[1]], [headPosition[0], headPosition[1]]],
    [[headPosition[0] + armLength, headPosition[1]], [headPosition[0], headPosition[1]]]
]);

