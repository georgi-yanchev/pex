# Copyright 2017 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pex.platforms import Platform


class TestPlatform(object):
  def test_platform(self):
    assert Platform('linux-x86_64', 'cp', '27', 'mu') == ('linux_x86_64', 'cp', '27', 'cp27mu')
    assert str(
      Platform('linux-x86_64', 'cp', '27', 'm')
    ) == 'linux_x86_64-cp-27-cp27m'
    assert str(Platform('linux-x86_64')) == 'linux_x86_64'

  def test_platform_create(self):
    assert Platform.create('linux-x86_64') == ('linux_x86_64', None, None, None)
    assert Platform.create('linux-x86_64-cp-27-cp27mu') == ('linux_x86_64', 'cp', '27', 'cp27mu')
    assert Platform.create('linux-x86_64-cp-27-mu') == ('linux_x86_64', 'cp', '27', 'cp27mu')
    assert Platform.create(
      'macosx-10.4-x86_64-cp-27-m') == ('macosx_10_4_x86_64', 'cp', '27', 'cp27m')

  def test_platform_create_noop(self):
    existing = Platform.create('linux-x86_64')
    assert Platform.create(existing) == existing

  def test_platform_current(self):
    assert Platform.create('current') == Platform.current()

  def test_platform_supported_tags(self):
    def test_tags(platform, expected_tags, manylinux=None):
      tags = Platform.create(platform).supported_tags(manylinux)
      for expected_tag in expected_tags:
        assert expected_tag in tags

    EXPECTED_BASE = [('py27', 'none', 'any'), ('py2', 'none', 'any')]

    test_tags(
      'linux-x86_64-cp-27-mu',
      EXPECTED_BASE + [('cp27', 'cp27mu', 'linux_x86_64')]
    )

    test_tags(
      'linux-x86_64-cp-27-mu',
      EXPECTED_BASE + [('cp27', 'cp27mu', 'manylinux1_x86_64')],
      True
    )

    test_tags(
      'macosx-10.4-x86_64',
      EXPECTED_BASE + [('cp27', 'cp27m', 'macosx_10_4_x86_64')]
    )

    test_tags(
      'macosx-10.12-x86_64-cp-27-m',
      EXPECTED_BASE + [
        ('cp27', 'cp27m', 'macosx_10_4_x86_64'),
        ('cp27', 'cp27m', 'macosx_10_5_x86_64'),
        ('cp27', 'cp27m', 'macosx_10_6_x86_64'),
        ('cp27', 'cp27m', 'macosx_10_7_x86_64'),
        ('cp27', 'cp27m', 'macosx_10_8_x86_64'),
        ('cp27', 'cp27m', 'macosx_10_9_x86_64'),
        ('cp27', 'cp27m', 'macosx_10_10_x86_64'),
        ('cp27', 'cp27m', 'macosx_10_11_x86_64'),
        ('cp27', 'cp27m', 'macosx_10_12_x86_64'),
      ]
    )
