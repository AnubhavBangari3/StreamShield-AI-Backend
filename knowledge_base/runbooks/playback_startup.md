# Slow Playback Startup

## Symptoms

- Startup time above 5 seconds
- Viewer abandonment
- Slow buffering before playback

## Possible Causes

- High CDN latency
- Large manifest
- Origin overload
- DNS delays

## Recommended Actions

1. Optimize manifest size.
2. Enable CDN prefetch.
3. Reduce startup bitrate.
4. Optimize DNS routing.
5. Increase origin capacity.

## Verification

Startup time should remain below 2 seconds.