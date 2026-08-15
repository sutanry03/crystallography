from cecvm.cluster_common import Cluster

def test_make_cluster():
    single = Cluster(((0., 0.5, 0.5),))
    assert len(single.slides) == 1