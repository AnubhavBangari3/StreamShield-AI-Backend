# CDN Failure Runbook

## Symptoms

- High CDN latency
- HTTP 5xx errors
- Regional playback failures
- Increased startup time

## Possible Causes

- CDN POP outage
- DNS routing issues
- Origin server overload
- Cache synchronization failure

## Recommended Actions

1. Route traffic to another CDN region.
2. Purge corrupted cache.
3. Check origin server health.
4. Verify CDN provider status.
5. Notify CDN operations team.

## Verification

Latency should return below 200 ms.