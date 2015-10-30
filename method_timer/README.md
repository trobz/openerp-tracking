## Introduction

This module aims to record the execution time of any method, it's a little bit
intrusive because tracking has to be explicitly define with a decorator but
it's the only constraint.

## Usage

- install the module on Odoo
- add the decorator on the method you want to track:
```python
from openerp.addons.method_timer.tracker.decorator import track
...

    @track(warning=10, critical=60)
    def button_fill_inventory(self, cr, uid, ids, context=None):
...
```
- restart your application

You should see some additional Odoo log with the execution time of this method.

## How it works

The idea is simple, use a decorator to get the time before and after the
method execution and get the diff.

Then [Record][R] object populated with all the useful information is passed
to a connector that will define the method to store these values.

**Warning**: the impact on performance should be limited, but still exists.
It depends on the type of connector and number of calls to the method,
[Redis][redis] should be fast but a custom connector recording to a file
may have more impact.

## Connectors

The module implement different type of connector for different propose.

Connectors are configured in the Odoo config file, see below the configuration
for each type of connector.


### Log connector (default)

This connector is simply logging the result with the same log facility than
Odoo.

#### Configuration

```
tracker_name = foo ; required, instance indentifier, usually the instance name
tracker_connector = log ; default value, not required
```

### Redis connector

To keep a trace of the execution time, data recorded can be stored in
a [Redis][redis] database, then an external tool can extract useful information.

For example, a [Check MK plugin][ck_method_timer] exists to method execution time
displayed as chart on Check MK interface.

Look at [how to setup local checks on Check MK][ck_timer_setup] to make metrics
available on Check MK.

#### Configuration

```
tracker_name = foo ; required, instance indentifier, usually the instance name
tracker_connector = redis
; Redis connection parameters
tracker_connector_redis_host = localhost
tracker_connector_redis_port = 6379
tracker_connector_redis_db = 0
```

### Custom Connector

It's possible to add new type of connector to store the recorded values
somewhere else.

The connector need to inherit from
`openerp.addons.method_timer.connector.core.Connector` and
implement at least the method `configure` and `commit`.
Please, check the [LogConnector][LC] source as an example to get more details.

Then, your custom connector need to be registered in the [ConnectorFactory][CF]
like this:
```python
from openerp.addons.method_timer.connector import connector_factory
...
connector_factory.register('foo', FooConnector)
```

Finally, you must change your Odoo configuration to use it:
```
tracker_connector = foo ; type of tracking connector
# these parameters will be passed as argument at FooConnector instantiation
# ie: connector = FooConnector(param1='bar', param2='foobar')
tracker_connector_foo_param1 = bar
tracker_connector_foo_param2 = foobar
```


 [redis]: http://redis.io/
 [ck_method_timer]: https://gitlab.trobz.com/sysadmin/check_mk-agent/blob/master/local/openerp_method_timer
 [ck_timer_setup]: https://sites.google.com/a/trobz.com/sysadmin/configuration/monitoring/check-mk-setup-local-checks
 [LC]: connector/log_connector.py
 [R]: tracker/record.py
 [CF]: connector/core.py