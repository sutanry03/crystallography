from cecvm.cluster_common import Cluster

def test_make_cluster():
    single = Cluster(((0., 0.5, 0.5),), [[0],[0],[0]])
    assert single.slides == (((0., 0., 0.),),)
    assert single.subclusters == ((),)