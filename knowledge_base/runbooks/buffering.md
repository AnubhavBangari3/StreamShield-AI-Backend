# Buffering Troubleshooting Guide

## Symptoms

- High buffering ratio
- Video pauses frequently
- Playback interruptions
- Viewer complaints increase

## Possible Causes

- Insufficient CDN bandwidth
- High packet loss
- Network congestion
- Bitrate too high

## Recommended Actions

1. Reduce video bitrate.
2. Check CDN edge node health.
3. Verify packet loss between origin and edge.
4. Increase CDN capacity if utilization exceeds 80%.
5. Monitor buffering ratio after mitigation.

## Verification

Buffer ratio should remain below 5%.