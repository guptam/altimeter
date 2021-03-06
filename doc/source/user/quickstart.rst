Quickstart
==========

This quickstart guide demonstrates how to generate a graph for a single account.

Installation
------------

::

    pip install altimeter

Configuration
-------------

Altimeter's behavior is driven by a toml configuration file.  A few sample
configuration files are included in the `conf/` directory:

* `current_single_account.toml` - scans the current account - this is the account
  for which the environment's currently configured AWS CLI credentials are.

* `current_master_multi_account.toml` - scans the current account and attempts to
  scan all organizational subaccounts - this configuration should be used if you
  are scanning  all accounts in an organization.  To do this the currently
  configured AWS CLI credentials should be pointing to an AWS Organizations
  master account.

To scan a subset of regions, set the region list parameter `regions` in the `scan`
section to a list of region names.

Generating the Graph
--------------------

Assuming you have configured AWS CLI credentials
(see <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html>),
run:

    altimeter <path-to-config>

This will scan all resources in regions specified in the config file.

The full path to the generated RDF file will printed, for example:

    Created /tmp/altimeter/20191018/1571425383/graph.rdf

This RDF file can then be loaded into a triplestore such as Neptune or Blazegraph for querying.

Tooling is included for loading into a local Blazegraph instance, see
:doc:`Local Querying with Blazegraph <local_blazegraph>`

