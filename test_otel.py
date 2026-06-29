from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer('test')
with tracer.start_as_current_span('parent') as p:
    ctx = trace.set_span_in_context(p)
    print('parent:', p.get_span_context().trace_id)
    with tracer.start_as_current_span('child', context=ctx) as c:
        print('child:', c.get_span_context().trace_id)
