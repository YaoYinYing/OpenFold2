from typing import Dict
import torch
import argparse
from pathlib import Path
import pickle
import numpy as np
from alphafold.Model import model_config
import numpy as np
from collections import namedtuple

from alphafold.Model.msa import Attention, MSARowAttentionWithPairBias, MSAColumnAttention, GlobalAttention, MSAColumnGlobalAttention
from alphafold.Model.spatial import TriangleAttention, TriangleMultiplication, OuterProductMean, Transition
from alphafold.Model.alphafold import EvoformerIteration, EmbeddingsAndEvoformer
from alphafold.Model.embedders import ExtraMSAEmbedding

from alphafold.Tests.utils import load_data, check_recursive

def AttentionTest(args, config, global_config):
	feat, params, res = load_data(args, 'Attention')
	# for param in params['attention'].keys():
	# 	print(param)
		
	conf = config.model.embeddings_and_evoformer.evoformer.msa_row_attention_with_pair_bias
	# conf.gating = False
	attn = Attention(conf, global_config, output_dim=256, key_dim=feat['q_data'].shape[-1], value_dim=feat['m_data'].shape[-1])
	attn.load_weights_from_af2(params['attention'], None)
	this_res = attn(q_data=feat['q_data'], m_data=feat['m_data'], bias=feat['bias'], nonbatched_bias=feat['nonbatched_bias'])
	
	check_recursive(this_res, res)

def MSARowAttentionWithPairBiasTest(args, config, global_config):
	feat, params, res = load_data(args, 'MSARowAttentionWithPairBias')
	# for key in params.keys():
	# 	print(key)
	# 	for param in params[key].keys():
	# 		print('\t' + param)
	conf = config.model.embeddings_and_evoformer.evoformer.msa_row_attention_with_pair_bias
	# conf.gating = False
	attn = MSARowAttentionWithPairBias(conf, global_config, pair_dim=feat['pair_act'].shape[-1], msa_dim=feat['msa_act'].shape[-1])
	attn.load_weights_from_af2(params, rel_path='msa_row_attention_with_pair_bias')
	this_res = attn(feat['msa_act'], feat['msa_mask'], feat['pair_act'])
	
	check_recursive(this_res, res)

def MSAColumnAttentionTest(args, config, global_config):
	feat, params, res = load_data(args, 'MSAColumnAttention')
	conf = config.model.embeddings_and_evoformer.evoformer.msa_column_attention
	attn = MSAColumnAttention(conf, global_config, msa_dim=feat['msa_act'].shape[-1])

	attn.load_weights_from_af2(params, rel_path='msa_column_attention')
	this_res = attn(feat['msa_act'], feat['msa_mask'])
	
	check_recursive(this_res, res)

def GlobalAttentionTest(args, config, global_config):
	feat, params, res = load_data(args, 'GlobalAttention')
			
	conf = config.model.embeddings_and_evoformer.evoformer.msa_row_attention_with_pair_bias
	attn = GlobalAttention(conf, global_config, output_dim=256, key_dim=feat['q_data'].shape[-1], value_dim=feat['m_data'].shape[-1])
	attn.load_weights_from_af2(params['attention'], None)
	this_res = attn(q_data=feat['q_data'], m_data=feat['m_data'], q_mask=feat['q_mask'], bias=feat['bias'])
	
	check_recursive(this_res, res)

def MSAColumnGlobalAttentionTest(args, config, global_config):
	feat, params, res = load_data(args, 'MSAColumnGlobalAttention')
	conf = config.model.embeddings_and_evoformer.evoformer.msa_column_attention
	attn = MSAColumnGlobalAttention(conf, global_config, msa_dim=feat['msa_act'].shape[-1])

	attn.load_weights_from_af2(params, rel_path='msa_column_global_attention')
	this_res = attn(feat['msa_act'], feat['msa_mask'])
	
	check_recursive(this_res, res)

def TriangleAttentionTest(args, config, global_config):
	feat, params, res = load_data(args, 'TriangleAttention')
	conf = config.model.embeddings_and_evoformer.evoformer.triangle_attention_starting_node
	attn = TriangleAttention(conf, global_config, pair_dim=feat['pair_act'].shape[-1])
	for key in params.keys():
		print(key)
		for param in params[key].keys():
			print('\t' + param)
	attn.load_weights_from_af2(params, rel_path='triangle_attention')
	this_res = attn(feat['pair_act'], feat['pair_mask'])
	
	check_recursive(this_res, res)

def TriangleMultiplicationOutgoingTest(args, config, global_config):
	feat, params, res = load_data(args, 'TriangleMultiplicationOutgoing')
	conf = config.model.embeddings_and_evoformer.evoformer.triangle_multiplication_outgoing
	attn = TriangleMultiplication(conf, global_config, pair_dim=feat['pair_act'].shape[-1])
	
	attn.load_weights_from_af2(params, rel_path='triangle_multiplication')
	this_res = attn(feat['pair_act'], feat['pair_mask'])
	
	check_recursive(this_res, res)

def TriangleMultiplicationIncomingTest(args, config, global_config):
	feat, params, res = load_data(args, 'TriangleMultiplicationIncoming')
	conf = config.model.embeddings_and_evoformer.evoformer.triangle_multiplication_incoming
	attn = TriangleMultiplication(conf, global_config, pair_dim=feat['pair_act'].shape[-1])
	
	attn.load_weights_from_af2(params, rel_path='triangle_multiplication')
	this_res = attn(feat['pair_act'], feat['pair_mask'])
	
	check_recursive(this_res, res)

def OuterProductMeanTest(args, config, global_config):
	feat, params, res = load_data(args, 'OuterProductMean')
	conf = config.model.embeddings_and_evoformer.evoformer.outer_product_mean
	attn = OuterProductMean(conf, global_config, msa_dim=feat['msa_act'].shape[-1], num_output_channel=256)
	for key in params.keys():
		print(key)
		for param in params[key].keys():
			print('\t' + param)
	attn.load_weights_from_af2(params, rel_path='outer_product_mean')
	this_res = attn(feat['msa_act'], feat['msa_mask'])
	
	check_recursive(this_res, res)

def TransitionTest(args, config, global_config):
	feat, params, res = load_data(args, 'Transition')
	conf = config.model.embeddings_and_evoformer.evoformer.pair_transition
	attn = Transition(conf, global_config, num_channel=feat['seq_act'].shape[-1])
	for key in params.keys():
		print(key)
		for param in params[key].keys():
			print('\t' + param)
	attn.load_weights_from_af2(params, rel_path='transition_block')
	this_res = attn(feat['seq_act'], feat['seq_mask'])
	
	check_recursive(this_res, res)

def EvoformerIterationTest1(args, config, global_config):
	feat, params, res = load_data(args, 'EvoformerIteration1')
	conf = config.model.embeddings_and_evoformer.evoformer
	
	attn = EvoformerIteration(conf, global_config, msa_dim=feat['msa_act'].shape[-1], pair_dim=feat['pair_act'].shape[-1], is_extra_msa=False)
	attn.load_weights_from_af2(params, rel_path='evoformer_iteration')
	
	this_res = attn(msa_act=feat['msa_act'], pair_act=feat['pair_act'], msa_mask=feat['msa_mask'].float(), pair_mask=feat['pair_mask'].float(), 
					is_training=False)
	this_res = {'msa':this_res[0],
				'pair':this_res[1]}
	check_recursive(this_res, res)
	

def EvoformerIterationTest2(args, config, global_config):
	feat, params, res = load_data(args, 'EvoformerIteration2')
	conf = config.model.embeddings_and_evoformer.evoformer
	
	attn = EvoformerIteration(	conf, global_config, 
								msa_dim=feat['msa_act'].shape[-1], pair_dim=feat['pair_act'].shape[-1], is_extra_msa=True)
	attn.load_weights_from_af2(params, rel_path='evoformer_iteration')

	activations = {'msa': feat['msa_act'], 'pair': feat['pair_act']}
	masks = {'msa': feat['msa_mask'], 'pair': feat['pair_mask']}
	
	this_res = attn(msa_act=feat['msa_act'], pair_act=feat['pair_act'], msa_mask=feat['msa_mask'].float(), pair_mask=feat['pair_mask'].float(), 
					is_training=False)
	this_res = {'msa':this_res[0],
				'pair':this_res[1]}

	check_recursive(this_res, res)

def EmbeddingsAndEvoformerTest(args, config, global_config, cuda:bool=False):
	feat, params, res = load_data(args, 'EmbeddingsAndEvoformer')
	conf = config.model.embeddings_and_evoformer
	for key in params.keys():
		print(key)
		for param in params[key].keys():
			print('\t' + param + '  ' + str(params[key][param].shape))
	for key in feat.keys():
		print(key, feat[key].shape)

	conf.template.enabled = False
	conf.recycle_pos = False
	conf.recycle_features = False
	conf.evoformer_num_block = 1
	conf.extra_msa_stack_num_block = 1
	global_config.deterministic = True
	attn = EmbeddingsAndEvoformer(conf, global_config, 
								target_dim=feat['target_feat'].shape[-1], 
								msa_dim=feat['msa_feat'].shape[-1],
								extra_msa_dim=25, clear_cache=False)
	attn.load_weights_from_af2(params, rel_path='evoformer')
	
	if cuda:
		attn = attn.cuda()
		for key in feat.keys():
			if isinstance(feat[key], torch.Tensor):
				feat[key] = feat[key].to(device='cuda')
		
	this_res = attn(feat, is_training=False)
	check_recursive(this_res, res)

def create_extra_msa_features_test(args, config, global_config):
	feat, params, res = load_data(args, 'create_extra_msa_feature')
	conf = config.model.embeddings_and_evoformer
	# for key in params.keys():
	# 	print(key)
	# 	for param in params[key].keys():
	# 		print('\t' + param + '  ' + str(params[key][param].shape))
	for key in feat.keys():
		print(key, feat[key].shape)

	emb = ExtraMSAEmbedding(conf, global_config, msa_dim=feat['msa_feat'].shape[-1])
	this_res = emb.create_extra_msa_features(feat)
	check_recursive(this_res, res)		

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Train deep protein docking')	
	parser.add_argument('-debug_dir', default='/home/lupoglaz/Projects/Folding/alphafold/Debug', type=str)
		
	args = parser.parse_args()
	config = model_config('model_1')
	global_config = config.model.global_config

	# create_extra_msa_features_test(args, config, global_config)
	
	# AttentionTest(args, config, global_config)
	MSARowAttentionWithPairBiasTest(args, config, global_config)
	# MSAColumnAttentionTest(args, config, global_config)
	# GlobalAttentionTest(args, config, global_config)
	# MSAColumnGlobalAttentionTest(args, config, global_config)
	# TriangleAttentionTest(args, config, global_config)
	# TriangleMultiplicationIncomingTest(args, config, global_config)
	# TriangleMultiplicationOutgoingTest(args, config, global_config)
	# OuterProductMeanTest(args, config, global_config)
	# TransitionTest(args, config, global_config)
	# EvoformerIterationTest1(args, config, global_config)
	# EvoformerIterationTest2(args, config, global_config)
	
	# with torch.no_grad():
	# 	EmbeddingsAndEvoformerTest(args, config, global_config)
	
	

	

	
	