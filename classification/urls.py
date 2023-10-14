from django.urls import path, include
from rest_framework import routers
from classification import views

router = routers.DefaultRouter()
router.register("nodes", views.NodeViewset)
router.register("facet", views.FacetViewset)
router.register("facet_category", views.FacetCategoryViewset)
router.register("sku_mappers", views.SKUMapperViewset),


urlpatterns = [
    path("", include(router.urls)),   
    path('nodes-by-facets-value/<int:facet_id>/', views.nodes_by_facets_value),
    path('taxonomy-change-feed/nodes/', views.NodeChangeFeedView.as_view()),
    path('taxonomy-change-feed/facets/', views.FacetChangeFeedView.as_view()),
    path('taxonomy-change-feed/relationships/', views.NodeFacetRelationshipChangeFeedView.as_view()),
    path('manufacturers/', views.ManufacturerView.as_view())
]
